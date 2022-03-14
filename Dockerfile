# I used fedora:34 rather than fedora:35 as the base image because of
# https://bugzilla.redhat.com/show_bug.cgi?id=1988199.
# Comment 26 there points to an upstream RHEL bug, but I am not
# certain it is the same bug as I was experiencing [garrison].
FROM fedora:34

RUN dnf install -y git @development-tools gcc-c++ python3 python3-devel julia
RUN python3 -m pip install -U pip

WORKDIR /qiskit_alt

# Copy only requirements.txt at this point, so changes to other
# portions of this repository don't invalidate these image layers.
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN julia -e 'using Pkg; pkg"registry add https://github.com/Qiskit-Extensions/QuantumRegistry.git"'

COPY . .
RUN pip install -e .

ENV QISKIT_ALT_COMPILE=y
ENV QISKIT_ALT_DEPOT=n

RUN python3 -c "import qiskit_alt; qiskit_alt.project.ensure_init()"
RUN python3 -c "import qiskit_alt; qiskit_alt.project.compile()"
