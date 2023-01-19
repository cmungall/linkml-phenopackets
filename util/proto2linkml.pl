#!/usr/bin/perl -w
use YAML::Syck;
use strict;

my $id = $ARGV[0];
$id =~ s@.*/@@;
$id =~ s@\.proto@@;
my $url = "https://w3id.org/linkml/phenopackets/$id";

our @INLINED = qw(Abundance
Cohort
CytobandInterval
Dictionary
DoseInterval
Expression
Extension
ExternalReference
Family
Feature
File
GeneDescriptor
GenomicInterpretation
MedicalAction
Member
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
Biosample
Individual
Interpretation
    Measurement);

our %INLINED_H = map { ($_ => 1) }  @INLINED;

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

if ($id eq 'base') {
    $schema->{classes}->{'Dictionary'} = {comments=>["TODO"]};
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
    'map<string, string>' => 'Dictionary',
    );

my $level = 0;
my @elts = ();
my $desc = "";
my $c = {};
my $e = {};
my @stack = ();
my @oneofs = ();
my $pack;
my $current_class;
while(<>) {
    chomp;
    next if $_ eq "";
    my $top;
    if (@stack) {
        $top = $stack[-1];
    }
    else {
        $top = '';
    }
    if (m@^import ".*/(\w+)\.proto"@) {
        push(@{$schema->{imports}}, $1);
    }
    elsif (m@^\s*//\s*(.*)@) {
        if ($desc) {
            $desc .= " $1";
        }
        else {
            $desc = "$1";
        }
    }
    elsif (m@^\s*message\s+(\S+)\s+\{@) {
        $desc = fix_desc($desc);
        $c = {description=>$desc, attributes=>{}};
        $schema->{classes}->{$1} = $c;
        $current_class = $1;
        if ($1 eq 'Phenopacket') {
            $schema->{classes}->{'Phenopacket'}->{'tree_root'} = 'true';
        }
        $desc = '';
        push(@stack, 'c');
    }
    elsif (m@^\s*enum\s+(\S+)\s+\{@) {
        chomp $desc;
        $e = {description=>$desc, permissible_values=>{}};
        $schema->{enums}->{$1} = $e;
        $desc = '';
        push(@stack, 'e');
    }
    elsif (m@^\s*oneof\s+(\S+)\s+\{@) {
        chomp $desc;
        #$e = {description=>$desc, permissible_values=>{}};
        #$schema->{enums}->{$1} = $e;
        $desc = '';
        push(@stack, 'oneof');
    }
    elsif ($top eq 'e' && m@^\s+(\S+)\s+=\s+(\d+);@) {
        chomp $desc;
        $e->{permissible_values}->{$1} = {description=>$desc};
        $desc = '';
    }
    elsif (m@deprecated=true@) {
    }
    elsif (($top eq 'c' || $top eq 'oneof') && m@^\s+(.*)\s+(\S+)\s+=\s+(\d+);@) {
        my ($range, $n, $ord) = ($1,$2,$3,$4);
        my $mv = 0;
        if ($range =~ m@repeated (\S+)@) {
            $range = $1;
            $mv = 1;
        }
        # VRS has fields like _Id
        if ($n eq '_id') {
            $n = 'id';
        }
        if ($n =~ m@^_@) {
            $n =~ s@^_@@;
        }
        while ($n =~ m@_@) {
            $n =~ s@_(\w)@uc($1)@e;
        }
        $range =~ s@.*\.@@; ## google.protobuf.Timestamp -> Timestamp
        if ($RMAP{$range}) {
            $range = $RMAP{$range}
        }
        if ($range eq 'Any') {
            $range = "string";
        }
        chomp $desc;
        $c->{attributes}->{$n} = {range=>$range, description=>$desc, annotations=>{rank=>$ord}};
        if ($mv) {
            $c->{attributes}->{$n}->{multivalued} = 'true';
        }
        if ($n eq 'id') {
            if ($desc =~ m@REQUIRED@) {
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
        if ($desc =~ m@REQUIRED@) {
            $c->{attributes}->{$n}->{required} = 'true';
        }
        if ($desc =~ m@ARGO mapping (\S+)::(\S+)@) {
            $c->{attributes}->{$n}->{exact_mappings} = ["ARGO:$1.$2"]
        }
        $desc = '';
        if ($top eq 'oneof') {
            push(@oneofs, $n);
        }
        if ($range =~ m@^[A-Z]@) {
            if ($range !~ m@String!@) {
                #$c->{attributes}->{$n}->{inlined} = 'true';
            }
        }
        if ($INLINED_H{$range}) {
            $c->{attributes}->{$n}->{inlined} = 'true';
        }
    }
    elsif (m@^\s*\}@) {
        my $popped = pop @stack;
        if (!@stack) {
            $c = {};
            $e = {};
        }
        if ($popped eq 'oneof') {
            my @conds = map { {slot_conditions=>{$_=>{required => 'true'}}} } @oneofs;
            $c->{rules} = [{
                postconditions => {
                    exactly_one_of => \@conds
                }
                           }];
            @oneofs = ();
        }
    }
    elsif (m@syntax = "(\S+)";@) {
        die unless $1 eq 'proto3';
    }
    elsif (m@package\s+(\S+);@) {
        $pack = $1;
    }
    elsif (m@option\s+(\S+)\s+=(.*);@) {
    }
    else {
        warn "UNP: $_\n";
    }
}

foreach (@elts) {
#    $schema->{classes}->{$_->{name}} = $_;
}

my $s = Dump($schema);
$s =~ s@\-\-\-@@;
$s =~ s@: 'true'@: true@g;
print $s;


sub fix_desc {
    my $desc = shift;
    chomp $desc;
    $desc =~ s@^Protocol Buffers.*POSSIBILITY OF SUCH DAMAGE\.\s+@@;
    return $desc;
}
