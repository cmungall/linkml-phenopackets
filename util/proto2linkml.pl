#!/usr/bin/perl -w
use YAML::Syck;
use Getopt::Long;
use strict;

# Usage: proto2linkml.pl [--source URL] FILE.proto > FILE.yaml
#
#   --source   URL of the .proto file that was converted, which becomes the
#              `source` of the schema. Only used for the root module.
#
# This is not a general protobuf parser. It handles the constructs that are used
# in phenopacket-schema, one statement per line, and stops at anything else.
my $schema_source;
GetOptions("source=s" => \$schema_source)
    or die "Usage: $0 [--source URL] FILE.proto\n";

my $id = $ARGV[0];
$id =~ s@.*/@@;
$id =~ s@\.proto@@;
my $url = "https://w3id.org/linkml/phenopackets/$id";

our @INLINED = qw(Abundance
Cohort
CytobandInterval
Disease
DoseInterval
Expression
Extension
ExternalReference
Family
Feature
File
GeneDescriptor
GenomicInterpretation
HaplotypeMember
MedicalAction
MetaData
MolecularVariation
OntologyClass
Person
Phenopacket
PhenotypicFeature
Resource
SequenceExpression
SequenceState
SimpleInterval
SystemicVariation
TimeElement
TimeInterval
TypedQuantity
Update
UtilityVariation
VariationSetMember
Biosample
Individual
Interpretation
    Measurement);

our %INLINED_H = map { ($_ => 1) }  @INLINED;

# A protobuf `map<string, string>` field is shorthand for a repeated entry message
# with a `key` (field 1) and a `value` (field 2). It is translated to a multivalued
# attribute that is inlined as a dictionary of entries of this class. LinkML accepts
# such a dictionary in the compact {key: value} form that protobuf uses in JSON.
my $MAP_ENTRY_CLASS = 'DictionaryEntry';

my $schema = {
    id => "$url",
    name => $id,
    default_prefix => $id,
    description => "Automatic translation of phenopackets protobuf to LinkML. Status: EXPERIMENTAL.",
    prefixes =>
    {
        'linkml' => 'https://w3id.org/linkml/',
            'argo' => 'https://docs.icgc-argo.org/dictionary/',
            $id => "$url/",
            'MONDO' => 'http://purl.obolibrary.org/obo/MONDO_',
            'UBERON' => 'http://purl.obolibrary.org/obo/UBERON_',
            'NCIT' => 'http://purl.obolibrary.org/obo/NCIT_',
            'GENO' => 'http://purl.obolibrary.org/obo/GENO_',
            'HP' => 'http://purl.obolibrary.org/obo/HP_',
            'UO' => 'http://purl.obolibrary.org/obo/UO_',
            'LOINC' => 'https://loinc.org/',
            'UCUM' => 'http://unitsofmeasure.org/',
    },
    imports => ['linkml:types'],
    classes => {},
    slots => {},
    enums => {},
    #types => {
    #    'IdentifierString'=>{
    #        'typeof'=>'string',
    #            'annotations'=>{'percent_encoded'=>'true'}
    #        },
    #},
};
$schema->{source} = $schema_source if defined $schema_source;

if ($id eq 'base') {
    $schema->{classes}->{$MAP_ENTRY_CLASS} = {
        description => "An entry of a protobuf map<string, string> field. An attribute that holds a map is multivalued and inlined as a dictionary of its entries, which can be written as {key: value, ...}",
        attributes => {
            key => {
                range => 'string',
                key => 'true',
                description => 'The key of the map entry. Keys are unique within a map.',
                annotations => {rank => 1},
            },
            value => {
                range => 'string',
                description => 'The value of the map entry.',
                annotations => {rank => 2},
            },
        },
    };
}
if ($id eq 'phenopackets') {
    push(@{$schema->{imports}}, "cv_terms")
}

my %RMAP = (
    'bool' => 'boolean',
    'uint32' => 'integer',
    'uint64' => 'integer',
    'bytes' => 'string',
    'int32' => 'integer',
    'int64' => 'integer',
    'Timestamp' => 'string',   # https://github.com/linkml/linkml/issues/629
    );

my $MESSAGE = qr@^\s*message\s+(\w+)\s*\{\s*$@;
my $ENUM = qr@^\s*enum\s+(\w+)\s*\{\s*$@;
my $ONEOF = qr@^\s*oneof\s+(\w+)\s*\{\s*$@;
my $CLOSE = qr@^\s*\}\s*;?\s*$@;

my @lines = <>;
foreach (@lines) {
    s@\r?\n$@@;
}

# Pre-scan the declarations. A nested message is normally given its simple name
# (Pedigree.Person => Person). When the same simple name is declared more than
# once in the file (Haplotype.Member and VariationSet.Member in VRS) the names of
# the enclosing messages are prepended (HaplotypeMember, VariationSetMember), so
# that no two messages of the file are translated to the same class.
my %msg_count = ();   # simple message name => number of declarations in this file
my %enum_count = ();  # simple enum name => number of declarations in this file
my %scoped = ();      # "Enclosing.Messages" => { simple name => class name }
{
    foreach (@lines) {
        my ($code) = split_comment($_);
        if ($code =~ m@^\s*(?:message|enum|oneof)\b.*\{.*\}@) {
            die "$id.proto: a block that is opened and closed on one line is not supported: $_\n";
        }
        $msg_count{$1}++ if $code =~ $MESSAGE;
        if ($code =~ $ENUM && ++$enum_count{$1} > 1) {
            die "$id.proto: more than one enum is called $1, which is not supported\n";
        }
    }
    my @scan = ();    # '' for enum/oneof blocks, otherwise the message name
    foreach (@lines) {
        my ($code) = split_comment($_);
        if ($code =~ $MESSAGE) {
            my $proto_name = $1;
            my @parents = grep { $_ ne '' } @scan;
            $scoped{join('.', @parents)}->{$proto_name} = class_name($proto_name, @parents);
            push(@scan, $proto_name);
        }
        elsif ($code =~ $ENUM || $code =~ $ONEOF) {
            push(@scan, '');
        }
        elsif ($code =~ $CLOSE) {
            pop(@scan);
        }
    }
}

# Comments are attributed to elements following the rules of protoc:
#  - a comment directly above an element is its description (leading comment)
#  - a comment on the same line as an element, or else one directly below it that
#    is followed by a blank line or by the end of the block, belongs to that
#    element (trailing comment)
#  - other comment blocks, separated by blank lines on both sides, are kept as
#    comments of the next element (detached comments)
my $desc = "";
my @detached = ();     # comment blocks separated from the next element by a blank line
my $prev;              # the element declared on the previous line, if any
my $c = {};
my $e = {};
my @stack = ();
my @cstack = ();       # enclosing [class, class name] pairs of the current message
my @mstack = ();       # protobuf names of the current message and its enclosing messages
my @oneofs = ();
my $oneof = {};
my %pv_order = ();     # enum name => permissible values in declaration order
my $current_enum;
my $pack;
my $current_class;
foreach (@lines) {
    if (m@^\s*$@) {
        if ($desc ne '') {
            if ($prev) {
                add_trailing_comment($prev, $desc);
            }
            else {
                push(@detached, $desc);
            }
            $desc = '';
        }
        $prev = undef;
        next;
    }
    if (m@^\s*//\s*(.*)@) {
        if ($desc ne '') {
            $desc .= " $1";
        }
        else {
            $desc = "$1";
        }
        next;
    }
    my $top;
    if (@stack) {
        $top = $stack[-1];
    }
    else {
        $top = '';
    }
    # $new is the element that this line declares, if any
    my $new;
    my ($code, $trailing) = split_comment($_);
    if ($code =~ m@^\s*import\s+(?:public\s+|weak\s+)?"(?:.*/)?(\w+)\.proto"\s*;\s*$@) {
        push(@{$schema->{imports}}, $1);
    }
    elsif ($code =~ $MESSAGE) {
        my $proto_name = $1;
        my $name = class_name($proto_name, @mstack);
        $desc = fix_desc($desc);
        push(@cstack, [$c, $current_class]);
        push(@mstack, $proto_name);
        $c = {description=>$desc, attributes=>{}};
        $c->{comments} = [@detached] if @detached;
        $schema->{classes}->{$name} = $c;
        $current_class = $name;
        if ($name eq 'Phenopacket') {
            $schema->{classes}->{'Phenopacket'}->{'tree_root'} = 'true';
        }
        $new = $c;
        push(@stack, 'c');
    }
    elsif ($code =~ $ENUM) {
        $current_enum = $1;
        chomp $desc;
        $e = {description=>$desc, permissible_values=>{}};
        $e->{comments} = [@detached] if @detached;
        $schema->{enums}->{$current_enum} = $e;
        $pv_order{$current_enum} = [];
        $new = $e;
        push(@stack, 'e');
    }
    elsif ($code =~ $ONEOF) {
        my $oneof_name = $1;
        chomp $desc;
        $oneof = {name=>$oneof_name, description=>$desc, comments=>[@detached]};
        $new = $oneof;
        push(@stack, 'oneof');
    }
    elsif ($top eq 'e' && $code =~ m@^\s*(\w+)\s*=\s*(-?\d+)\s*(\[[^\]]*\])?\s*;\s*$@) {
        my ($value, $number, $opts) = ($1, $2, $3);
        chomp $desc;
        # the number of an enum value is recorded in the same way as a field number
        my $pv = {description=>$desc, annotations=>{rank=>$number}};
        $pv->{comments} = [@detached] if @detached;
        $pv->{deprecated} = deprecation() if is_deprecated($opts);
        $e->{permissible_values}->{$value} = $pv;
        push(@{$pv_order{$current_enum}}, $value);
        $new = $pv;
    }
    elsif (($top eq 'c' || $top eq 'oneof') && $code =~ m@^\s*(\S.*?)\s+(\w+)\s*=\s*(\d+)\s*(\[[^\]]*\])?\s*;\s*$@) {
        my ($range, $n, $ord, $opts) = ($1,$2,$3,$4);
        my $mv = 0;
        if ($range =~ s@^repeated\s+@@) {
            $mv = 1;
        }
        $range =~ s@^optional\s+@@;
        # Attributes are named after the protobuf JSON name of the field, which is
        # what a phenopacket in JSON/YAML uses (individual_id => individualId). The
        # VRS `_id` fields have the JSON name `Id`.
        if ($opts && $opts =~ m@\bjson_name\s*=\s*"([^"]+)"@) {
            $n = $1;
        }
        else {
            $n = json_name($n);
        }
        my $is_map = 0;
        if ($range =~ m@^map\s*<\s*string\s*,\s*string\s*>$@) {
            if ($id ne 'base' && !grep { $_ eq 'base' } @{$schema->{imports}}) {
                die "$id.proto: $current_class.$n is a map, but $id does not import base, which defines $MAP_ENTRY_CLASS\n";
            }
            $range = $MAP_ENTRY_CLASS;
            $mv = 1;
            $is_map = 1;
        }
        elsif ($range =~ m@^map\b@) {
            die "$id.proto: unsupported map type for $current_class.$n: $range\n";
        }
        else {
            ## google.protobuf.Timestamp -> Timestamp
            $range = resolve_range($range, @mstack);
        }
        if ($RMAP{$range}) {
            $range = $RMAP{$range}
        }
        if ($range eq 'Any') {
            $range = "string";
        }
        chomp $desc;
        my $attribute = {range=>$range, description=>$desc, annotations=>{rank=>$ord}};
        $attribute->{comments} = [@detached] if @detached;
        # a field that has a comment behind it cannot get another one below it
        $new = $attribute if $trailing eq '';
        if ($trailing ne '') {
            # the comment behind a field documents it when there is none above it
            add_trailing_comment($attribute, $trailing);
            $trailing = '';
        }
        $c->{attributes}->{$n} = $attribute;
        # the keywords in the documentation of the field
        my $doc = $attribute->{description};
        if ($mv) {
            $c->{attributes}->{$n}->{multivalued} = 'true';
        }
        if (is_deprecated($opts)) {
            $c->{attributes}->{$n}->{deprecated} = deprecation();
        }
        if ($n eq 'id') {
            if ($doc =~ m@REQUIRED@) {
                $c->{attributes}->{$n}->{identifier} = 'true';
            }
            else {
                warn "id for $current_class not required";
            }
            #$c->{attributes}->{$n}->{range} = 'IdentifierString';
            $c->{attributes}->{$n}->{range} = 'string';
            if ($current_class ne "OntologyClass") {
                $c->{attributes}->{$n}->{annotations}->{percent_encoded} = 'true';
            }
        }
        if ($doc =~ m@REQUIRED@) {
            $c->{attributes}->{$n}->{required} = 'true';
        }
        if ($doc =~ m@ARGO mapping (\S+)::(\S+)@) {
            $c->{attributes}->{$n}->{exact_mappings} = ["ARGO:$1.$2"]
        }
        if ($top eq 'oneof') {
            push(@oneofs, $n);
        }
        if ($range =~ m@^[A-Z]@) {
            if ($range !~ m@String!@) {
                #$c->{attributes}->{$n}->{inlined} = 'true';
            }
        }
        if ($is_map) {
            # inlined as a dictionary keyed by the entry key (not as a list)
            $c->{attributes}->{$n}->{inlined} = 'true';
        }
        elsif ($INLINED_H{$range}) {
            if ($mv) {
                $c->{attributes}->{$n}->{inlined_as_list} = 'true';
            }
            else {
                $c->{attributes}->{$n}->{inlined} = 'true';
            }
        }
    }
    elsif ($code =~ $CLOSE) {
        my $popped = pop @stack;
        if ($desc ne '' && $prev) {
            add_trailing_comment($prev, $desc);
            $desc = '';
        }
        # Comments left at the end of a block are notes about the element that is
        # being closed, not the description of whatever is declared next
        my @notes = @detached;
        push(@notes, $desc) if $desc ne '';
        if ($popped eq 'oneof') {
            # A message can have several oneofs: each one is translated to its own rule
            my @conds = map { {slot_conditions=>{$_=>{required => 'true'}}} } @oneofs;
            my $rule = {
                annotations => {oneof => $oneof->{name}},
                postconditions => {
                    exactly_one_of => \@conds
                }
            };
            push(@{$oneof->{comments}}, @notes);
            $rule->{description} = $oneof->{description} if $oneof->{description} ne '';
            $rule->{comments} = $oneof->{comments} if @{$oneof->{comments}};
            push(@{$c->{rules}}, $rule);
            @oneofs = ();
        }
        elsif ($popped eq 'c') {
            push(@{$c->{comments}}, @notes) if @notes;
            pop(@mstack);
            ($c, $current_class) = @{pop @cstack};
        }
        elsif ($popped eq 'e') {
            push(@{$e->{comments}}, @notes) if @notes;
            $e = {};
        }
    }
    elsif ($code =~ m@^\s*syntax\s*=\s*"(\S+)"\s*;@) {
        die "$id.proto: only proto3 is supported\n" unless $1 eq 'proto3';
    }
    elsif ($code =~ m@^\s*package\s+(\S+)\s*;@) {
        $pack = $1;
    }
    elsif ($code =~ m@^\s*option\s+(\S+)\s*=(.*);@) {
    }
    else {
        die "$id.proto: cannot parse this line: $_\n";
    }
    if ($new && $trailing ne '') {
        # the comment behind the declaration of a message, an enum, a oneof or an
        # enum value; nothing below it can then be a trailing comment as well
        add_trailing_comment($new, $trailing);
        $new = undef;
    }
    # the comments above this line have been used, or do not belong to anything
    $desc = '';
    @detached = ();
    $prev = $new;
}

# YAML::Syck sorts mapping keys, but the order of enum values is meaningful: the
# first value of a proto3 enum is its default. The permissible values are therefore
# emitted one by one, in declaration order, and spliced into the dumped schema.
my %pv_placeholder = ();
foreach my $enum_name (keys %{$schema->{enums}}) {
    my $en = $schema->{enums}->{$enum_name};
    my $placeholder = "PERMISSIBLE_VALUES_OF_$enum_name";
    $pv_placeholder{$placeholder} = [map { [$_, $en->{permissible_values}->{$_}] } @{$pv_order{$enum_name}}];
    $en->{permissible_values} = $placeholder;
}

my $s = Dump($schema);
$s =~ s@^( *)permissible_values: (PERMISSIBLE_VALUES_OF_\w+) *$@dump_permissible_values($1, $pv_placeholder{$2})@gme;
$s =~ s@\-\-\-@@;
# booleans are set as the string 'true' above
$s =~ s@^(\s*(?:identifier|inlined|inlined_as_list|key|multivalued|percent_encoded|required|tree_root): )'true'$@$1true@gm;
print $s;


sub fix_desc {
    my $desc = shift;
    chomp $desc;
    $desc =~ s@^Protocol Buffers.*POSSIBILITY OF SUCH DAMAGE\.\s+@@;
    return $desc;
}

# The statement on a line and the text of the // comment behind it. Statements
# that contain // themselves, in a string, are not supported.
sub split_comment {
    my $line = shift;
    if ($line =~ m@^(.*?)\s*//\s*(.*?)\s*$@) {
        return ($1, $2);
    }
    return ($line, '');
}

# A trailing comment documents an element that has no description of its own,
# and is an additional comment otherwise
sub add_trailing_comment {
    my ($element, $comment) = @_;
    if (!defined($element->{description}) || $element->{description} eq '') {
        $element->{description} = $comment;
    }
    else {
        push(@{$element->{comments}}, $comment);
    }
}

# Whether the options of a field or of an enum value, [...], mark it as deprecated
sub is_deprecated {
    my $opts = shift;
    return defined($opts) && $opts =~ m@\bdeprecated\s*=\s*true\b@;
}

sub deprecation {
    return 'Marked as deprecated (deprecated=true) in the protobuf definition';
}

# The JSON name protoc assigns to a field: underscores are removed and the
# character that follows an underscore is capitalized.
sub json_name {
    my $n = shift;
    my $out = '';
    my $capitalize = 0;
    foreach my $ch (split(//, $n)) {
        if ($ch eq '_') {
            $capitalize = 1;
        }
        elsif ($capitalize) {
            $out .= uc($ch);
            $capitalize = 0;
        }
        else {
            $out .= $ch;
        }
    }
    return $out;
}

# The class name of a message, given the names of the messages that enclose it
sub class_name {
    my ($name, @parents) = @_;
    if (@parents && $msg_count{$name} > 1) {
        return join('', @parents, $name);
    }
    return $name;
}

# The range for a type name that is used in a message. The name, which can be
# qualified with the messages that enclose the type (Member, Haplotype.Member), is
# looked up from the innermost enclosing message outwards. A name that starts with
# a package (org.ga4gh.vrs.v1.Haplotype.Member) ends with the enclosing messages.
# Types that are not messages of this file keep their simple name.
sub resolve_range {
    my ($type, @parents) = @_;
    my @qualifier = split(/\./, $type);
    my $name = pop(@qualifier);
    my @scopes = ();
    for (my $i = $#parents; $i >= -1; $i--) {
        push(@scopes, join('.', @parents[0..$i], @qualifier));
    }
    for (my $i = 1; $i <= $#qualifier; $i++) {
        push(@scopes, join('.', @qualifier[$i..$#qualifier]));
    }
    foreach my $scope (@scopes) {
        if ($scoped{$scope} && $scoped{$scope}->{$name}) {
            return $scoped{$scope}->{$name};
        }
    }
    return $name;
}

sub dump_permissible_values {
    my ($indent, $pvs) = @_;
    my $out = "${indent}permissible_values: \n";
    foreach my $pv (@$pvs) {
        my $block = Dump({$pv->[0] => $pv->[1]});
        $block =~ s@^\-\-\- *\n@@;
        $block =~ s@^@$indent  @gm;
        $out .= $block;
    }
    chomp $out;
    return $out;
}
