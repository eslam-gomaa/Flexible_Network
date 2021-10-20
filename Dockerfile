FROM python:3.6-buster
MAINTAINER eslam.gomaa
RUN mkdir test
WORKDIR test
RUN git clone https://github.com/eslam-gomaa/Flexible_Network.git
RUN cd Flexible_Network && python3.6 setup.py bdist_wheel
RUN pip3.6 install Flexible_Network/dist/FlexibleNetwork-*.whl

CMD /bin/bash
