all: gif mp4

splitgif:
	python splitter.py $(filename)

translation:
	python parser.py $(filename)

mp4: gif
	python gif2mp4.py

clean:
	rm -rf out/
