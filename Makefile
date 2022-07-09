CC = g++
CCSW = -O3 -Wno-deprecated-declarations
PLATFORM = `uname`

all:	lander spring

lander: lander.o lander_graphics.o
	@if [ ${PLATFORM} = "Linux" ]; \
	then $(CC) -o lander lander.o lander_graphics.o ${CCSW} -lGL -lGLU -lglut; \
	echo Linking for Linux; \
	elif [ ${PLATFORM} = "Darwin" ]; \
	then $(CC) -o lander lander.o lander_graphics.o ${CCSW} -framework GLUT -framework OpenGL; \
	echo Linking for Mac OS X; \
	else $(CC) -o lander lander.o lander_graphics.o ${CCSW} -lglut32 -lglu32 -lopengl32; \
	echo Linking for Cygwin; \
	fi

lander_graphics.o lander.o: lander.h

spring: spring.o

.cpp.o:
	$(CC) ${CCSW} -c $<

clean:
	echo cleaning up; /bin/rm -f core *.o lander spring
