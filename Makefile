# basename of a YAML file in model/
.PHONY: all clean

clean:
	rm -rf project
	rm -rf tmp

project/%.py: clean
	poetry run gen-project -d project model/$(subst .py,,$(subst project/,,$@)).yaml
