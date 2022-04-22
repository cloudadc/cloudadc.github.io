#! /bin/sh

echo If difficulty is encountered, please let us know in the academy channel on Calico Users Slack.

[[ "${AWS_EXECUTION_ENV}" != "CloudShell" ]] && { echo "Please use AWS CloudShell."; exit 1; }

[[ ! -d "`echo ~`/.local/bin" ]] && mkdir -p "`echo ~`/.local/bin"
[[ ! -f "`echo ~`/.ssh/id_rsa" ]] && (echo "Generating new ssh-keypair." && ssh-keygen -b 2048 -t rsa -f "`echo ~`/.ssh/id_rsa" -q -N "")

echo Downloading lab assets.
calicoctl -h &> /dev/null || (echo "Downloading calicoctl"; curl -Lo "`echo ~`/.local/bin/calicoctl" https://github.com/projectcalico/calicoctl/releases/download/v3.17.1/calicoctl-linux-amd64 )
kubectl -h &> /dev/null || (echo "Downloading kubectl"; curl -Lo "`echo ~`/.local/bin/kubectl" https://dl.k8s.io/release/v1.19.0/bin/linux/amd64/kubectl )
kops -h &> /dev/null || (echo "Downloading kOps"; curl -Lo "`echo ~`/.local/bin/kops" https://github.com/kubernetes/kops/releases/download/v1.19.0/kops-linux-amd64 )
verify &>/dev/null || (echo "Downloading verify"; curl -Lo "`echo ~`/.local/bin/verify" https://github.com/tigera/ccol1/releases/download/1.0/verify )
eksctl -h &> /dev/null || (echo "Downloading eksctl"; curl -Lo /tmp/eksctl.tgz https://github.com/weaveworks/eksctl/releases/download/0.48.0/eksctl_Linux_amd64.tar.gz && tar xzvf /tmp/eksctl.tgz > /dev/null && mv eksctl ~/.local/bin/eksctl )
chmod +x "`echo ~`/.local/bin/"*

echo Verifying installation.
calicoctl -h &> /dev/null || { echo "Error downloading calicoctl. Please try again."; rm -f "`echo ~`/.local/bin/calicoctl"; exit 1; }
kubectl -h &> /dev/null || { echo "Error downloading kubectl. Please try again."; rm -f "`echo ~`/.local/bin/kubectl"; exit 1; }
kops -h &> /dev/null || { echo "Error downloading kOps. Please try again."; rm -f "`echo ~`/.local/bin/kops"; exit 1; }
verify &> /dev/null ||  { echo "Error downloading verify. Please try again."; rm -f "`echo ~`/.local/bin/verify"; exit 1; }
eksctl -h &> /dev/null || { echo "Error downloading eksctl. Please try again."; rm -f "`echo ~`/.local/bin/eksctl"; exit 1; }
echo Installation complete.

exit 0
