




com = serial('COM3', 'BaudRate', 460800 );
fopen( com );

%fwrite(com, msg, 'uint8');
%out = fread(com, 10, 'uint8' )

%status = peregrine_query_status( com, 1 )

%peregrine_move( com, 1, 2000, 1500, 500 );

%peregrine_read( com, 1, 30 )
%peregrine_write( com, 1, 30, 1337 )
%peregrine_read( com, 1, 30 )

%peregrine_i2c_read_temperature( com, 1, 146 )

peregrine_mem_read( com, 1, 25 )
peregrine_mem_write( com, 1, 25, -1234 )
peregrine_mem_read( com, 1, 25 )


fclose( com );
delete( com );
clear com;