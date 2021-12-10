# This Dockerfile is a work-in-progress while we try to figure out
# the best way to provide a private ssh key to this build process
# https://github.ibm.com/John-Lapeyre/qiskit_alt/issues/8

FROM fedora:34

RUN dnf install -y git @development-tools gcc-c++ \
                   python3 python3-devel python3-pip julia
RUN pip install -U pip

WORKDIR /qiskit_alt

# Copy only requirements.txt for now, so changes to other portions of
# this repository don't invalidate these image layers.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Obtained by running `ssh-keyscan github.ibm.com`
RUN mkdir -p /root/.ssh && echo -e '\
github.ibm.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1K6pnwsCh8hFCqvzWkb1y3ajXervgfokIdZ/VIURIItVBIINtH5Ynupt2cLLBMYysYjR1I/P4VNZf7bX+HejjJqMf92psXQ1VToyKeNZ+i01CrhZko11157veidnMwVmKoCIdrKpsLgqthJ6kXLrTqaVIQ1sh3lKZ0tFRsqgiwNbstwhRZe/MyUoDuzHZQPooxsiy5dBO+LpkovCShwVfZ3380UyAfScPrUZcX2zY/qmGDz4puXOWj/CQupoe76JoVenfwrjfTw2I+GoPxpZK6R47akoAekCO+Dw8VW4NnTDR6L7eGkclltQSC7HQ9MiFDB4Z49ONWQwotLdttDr5\
github.ibm.com ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBC1Sg96+K5rc8ZTYhidXI1Q6qUBRgrC51I2pUop4xo4keH8r/5V1W+z2dZNKZsVLW12ulIAe9yorXt2MrI8V0XE=\
' >> /root/.ssh/known_hosts

COPY . .
RUN pip install -e .
RUN ln -fs /usr/bin/julia .
RUN python3 -c "import julia; julia.install()"
#RUN python3 -c "import qiskit_alt; qiskit_alt.compile_qiskit_alt()"
