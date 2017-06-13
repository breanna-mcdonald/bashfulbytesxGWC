DIRS = about resources

all: $(DIRS)

build:
	./gen.py
	staticjinja build > /dev/null 2>&1

$(DIRS): build
	cd $@/ && staticjinja build > /dev/null 2>&1

publish:
	./rss.py
	
clean:
	find . -name '.[!.]*[swo|swp]' -delete
