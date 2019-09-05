function status = peregrine_query_status( com, address )
    msg = [ address 3 0 0 0 0 0 0 0 0 ];
    fwrite(com, msg, 'uint8');
    response = fread(com, 10, 'uint8' );
    
    status.position = int32( swapbytes( typecast( uint8( response(3:6) ), 'int32' ) ) );
    status.speed = int16( swapbytes( typecast(uint8(response(7:8)), 'int16' ) ) );
    
    
    flags = uint16( swapbytes( typecast(uint8(response(9:10)), 'uint16' ) ) );
    
    %response'
    %flags
    
    flg_running = bitshift(1,0);
    flg_emg_stop = bitshift(1,1);
    flg_limit_plus = bitshift(1,2);
    flg_limit_minus = bitshift(1,3);
    flg_fdir = bitshift(1,4);
    flg_cl = bitshift(1,5);

    
    status.flags.running = bitand( flags, flg_running ) == flg_running;
    status.flags.emg_stop = bitand( flags, flg_emg_stop ) == flg_emg_stop;
    status.flags.limit_plus = bitand( flags, flg_limit_plus) == flg_limit_plus;
    status.flags.limit_minus = bitand( flags, flg_limit_minus ) == flg_limit_minus;
    status.flags.fdir = bitand( flags, flg_fdir ) == flg_fdir;
    status.flags.cl = bitand( flags, flg_cl ) == flg_cl;
    
    
    
end