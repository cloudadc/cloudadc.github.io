for limit in fsize cpu as memlock
do
  grep "root" /etc/security/limits.conf | grep -q $limit || echo -e "root     hard   $limit    unlimited\nroot     soft   $limit   unlimited" | sudo tee --append /etc/security/limits.conf
  grep "nginx" /etc/security/limits.conf | grep -q $limit || echo -e "nginx     hard   $limit    unlimited\nnginx     soft   $limit   unlimited" | sudo tee --append /etc/security/limits.conf
done

for limit in nofile noproc
do
  grep "root" /etc/security/limits.conf | grep -q $limit || echo -e "root     hard   $limit    64000\nroot     soft   $limit   64000" | sudo tee --append /etc/security/limits.conf
  grep "nginx" /etc/security/limits.conf | grep -q $limit || echo -e "nginx     hard   $limit    64000\nnginx     soft   $limit   64000" | sudo tee --append /etc/security/limits.conf
done
