#!/usr/bin/perl

system("/opt/rest/admin/stop_app.py $ARGV[0]");
sleep(5);
my $something = qx/netstat -tulpn | grep ':105'/;
sleep(15);
if(!$something){
	exec("/opt/rest/app.py &");	
}
