#Create a simulator object
set ns [new Simulator]

#Define different colors for data flows (for NAM)
$ns color 1 Blue
$ns color 2 Red

#Open the NAM trace file
set nf [open out.nam w]
$ns namtrace-all $nf

#Open the Trace file
set tf [open out.tr w]
$ns trace-all $tf

#Define a 'finish' procedure
proc finish {} {
        global ns nf tf
        $ns flush-trace
        #Close the NAM trace file
        close $nf
        #Close the Trace file
        close $tf
        #Execute NAM on the trace file
        exec nam out.nam &

	# Get data from trace file, put current-time and calculated-throughput in a new file
	exec awk {
      	{
      	if ( (($1=="r") && ($3=="2") && ($4=="3") && ($5=="cbr")) || (($1=="r") && ($3=="2") && ($4=="3") && ($5=="tcp")) ) {
              old_data=old_data + $6
              print $2, old_data*8.0/$2/1000000
       	}
       	}
	} out.tr > performance.data
	
	# Call xgraph plotting program to plot throughput vs time
	exec xgraph performance.data &


	# Get data from trace file, put current-time and drops in a new file
	exec awk {
      	{
      	if (($1=="d")) {
              old_data=old_data + 1
              print $2, old_data
       	}
       	}
	} out.tr > drops.data
	

	# Get data from trace file, put current-time and drops in a new file
	exec awk {
      	{
      	if ( (($1=="r") && ($3=="2") && ($4=="3") && ($5=="cbr")) || (($1=="r") && ($3=="2") && ($4=="3") && ($5=="tcp")) ) {
              old_data=old_data + 1
              print $2, old_data
       	}
       	}
	} out.tr > success.data


	# Call xgraph plotting program to plot throughput vs time
	exec xgraph drops.data success.data &   

	# Get data from trace file, put current-time and jitter in a new file
	exec awk {
      	{
      	if (($1=="r") && ($3=="2") && ($4=="3") && ($5=="cbr")) {
             print $2, ($2 - timeOld)
	     timeOld = $2
       	}
       	}
	} out.tr > jitter.data
	
	# Call xgraph plotting program to plot throughput vs time
	exec xgraph jitter.data  &

	exit 0
}

#Create four nodes
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]

#Create links between the nodes
$ns duplex-link $n0 $n2 2Mb 10ms DropTail
$ns duplex-link $n1 $n2 2Mb 10ms DropTail
$ns duplex-link $n2 $n3 1.7Mb 20ms DropTail

#Set Queue Size of link (n2-n3) to 10
$ns queue-limit $n2 $n3 10

#Give node position (for NAM)
$ns duplex-link-op $n0 $n2 orient right-down
$ns duplex-link-op $n1 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right

#Monitor the queue for link (n2-n3). (for NAM)
$ns duplex-link-op $n2 $n3 queuePos 0.5


#Setup a TCP connection
set tcp [new Agent/TCP]
$tcp set class_ 2
$ns attach-agent $n0 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n3 $sink
$ns connect $tcp $sink
$tcp set fid_ 1

#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP


#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n1 $udp
set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp $null
$udp set fid_ 2

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ 1mb
$cbr set random_ false


#Schedule events for the CBR and FTP agents
$ns at 0.1 "$cbr start"
$ns at 1.0 "$ftp start"
$ns at 4.0 "$ftp stop"
$ns at 4.5 "$cbr stop"

#Detach tcp and sink agents (not really necessary)
$ns at 4.5 "$ns detach-agent $n0 $tcp ; $ns detach-agent $n3 $sink"

#Call the finish procedure after 5 seconds of simulation time
$ns at 5.0 "finish"

#Print CBR packet size and interval
puts "CBR packet size = [$cbr set packet_size_]"
puts "CBR interval = [$cbr set interval_]"

#Run the simulation
$ns run



