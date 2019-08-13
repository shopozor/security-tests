FROM golang:1.9-stretch

COPY *.go /app
COPY *.py /app

WORKDIR /app

ENV ssllabs-scan /app


RUN go get -d -v ./...
RUN go install -v ./...

RUN go build


# returns the grade of the website, typically one of: A+, A, B, C, D, E, F
RUN python securityheaders-grade.py https://www.softozor.ch

# returns the grade of the website, typically one of: A+, A, B, C, D, E, F
RUN python ssllabs-grade.py https://www.softozor.ch

# TODO notification. If one of the two grades above is not A+, we need to be notified.

CMD ["app"]