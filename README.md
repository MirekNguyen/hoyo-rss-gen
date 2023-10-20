# Hoyo RSS Generator

Python script that creates an RSS feed by web scraping websites related to Genshin.

## Prerequisities

You can run the script in two ways

### 1. Using Docker:

-   Docker installed on your machine
-   docker-compose installed on your machine.

### 2. Using Python with pip

-   Python 3.x installed on your machine.
-   pip installed

## Building and Running with Docker

1. Navigate to the directory containing the docker-compose.yml.

```
cd <project>/docker
```

2. Run the service using the following command

```
docker-compose up -d
```

3. Alternatively, you can build it on your own using Dockerfile

-   Navigate to the root directory of the project

```
cd <project>
```

-   Build

```
docker build -t hoyo-rss -f docker/Dockerfile .
```

-   Run

```
docker run -v ./out:/out hoyo-rss -o /out/output.xml
```

## Output

Upon successful execution, the generated RSS feed will be available at:

```
<project>/out/output.xml
```
