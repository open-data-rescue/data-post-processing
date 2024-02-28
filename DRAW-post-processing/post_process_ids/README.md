# data-post-processing
code for post processing transcribed data


This repository contains code was started in summer 2022 by Nathan Leuranger and Victoria Slonosky to post-process presssure data from the McGill DRAW
transcription project https://draw.geog.mcgill.ca/.

# Deployment

There is a docker image containing the python code for this project. The packages are
released and tagged. To get the latest release you can pull the docker image from the
github repository using the commend:

`docker pull ghcr.io/open-data-rescue/data-post-processing:latest`

If you need a specific version replaces the `latest` tag with the version number.

There are 5 environment variables used to connect the code to the Draw MySQL database. These
are:

| Variable | Description | Example Value |
| ------------------- | -------------------------------------| ---------------|
| DRAW_local_db_user | The user name to connect to the db ||
| DRAW_local_db_pass | The user's DB password ||
| DRAW_local_db_name | The name of the DB schema | draw_production |
| DRAW_db_host | The host that the DB is running on | localhost |
| DRAW_db_port | The TCP port to connect (defaults tp 3306 if not set) | 3306 |

To run the data processing python script after you have pull the image use

```
  docker run \
    --env DRAW_local_db_user=draw_user \
    --env DRAW_local_db_pass=draw_user_password \
    --env DRAW_local_db_name=climate_data_rescue \
    --env DRAW_db_host=localhost \
    --env DRAW_db_port=3306 \
    -it --rm --network host \
    --mount type=bind,source="./SEF",target=/opt/draw-post-processing/SEF \
    ghcr.io/open-data-rescue/data-post-processing
```

## NOTES:

The SEF files will be put in the directory you specify within the mount command. Change the `./SEF` to a directory where you would like the SEF files to be placed.

Also set the DB user, password and name to match what you need to connect to you database.
