FROM continuumio/miniconda3
MAINTAINER Sharib Ali<sharib.ali@eng.ox.ac.uk> 

RUN conda create -n env python=3.6 numpy
RUN echo "source activate env" > ~/.bashrc

RUN mkdir /output/
RUN mkdir /input/

RUN chmod 777 /output/
RUN chmod 777 /input/

ENV PATH /opt/conda/envs/env/bin:$PATH

RUN conda install -c jmcmurray json 
RUN conda install -c conda-forge unzip 
RUN pip install tifffile
RUN pip install scikit-learn

# create user ead2019
RUN useradd --create-home -s /bin/bash EndoCV2020 
USER EndoCV2020

RUN mkdir -p /home/EndoCV2020/app 
WORKDIR /home/EndoCV2020/app

# add all evaluation and groundTruth directories
COPY EndoCV2020 EndoCV2020/ 
COPY groundTruths_EAD2019 groundTruths_EAD2020/

# add run script
COPY run_script.sh run_script.sh

RUN [ "/bin/bash", "-c", "source activate env"]

RUN mkdir /home/EndoCV2020/input/
RUN mkdir /home/EndoCV2020/output/

# uncomment this for testing
#COPY ead2019_testSubmission /input/ead2019_testSubmission

# COPY EndoCV2020_testSubmission/detection_bbox /input/detection_bbox
# COPY EndoCV2020_testSubmission/semantic_masks /input/semantic_masks
# COPY EndoCV2020_testSubmission/generalization_bbox /input/generalization_bbox

RUN pip install opencv-python==3.3.0.10
#ENTRYPOINT /bin/bash

ENTRYPOINT ["bash"]
CMD ["/home/EndoCV2020/app/run_script.sh"]


# docker run --mount source=ead2019_testSubmission.zip,target=/input -ti --rm  ead2019_v2:latest /bin/bash

# --mount source=ead2019_testSubmission.zip,target=/input -ti --rm  endocv2020:latest /bin/bash
# sudo docker build -t endocvleaderboard:latest . 
# sudo docker run -ti --rm endocvleaderboard:latest /bin/bash
# sudo docker save endocvleaderboard:latest | gzip -c > endocv2020.tar.gz
