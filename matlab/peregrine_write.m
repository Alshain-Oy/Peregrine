function result = peregrine_write( com, address, key, value )
    msg = [ address 1 0 0 0 0 0 0 0 0 ];
    msg(3:6) = uint8( typecast( swapbytes(uint32(key)), 'uint8') ) ;
    msg(7:10) = uint8( typecast( swapbytes(int32(value)), 'uint8') ) ;
    
    fwrite(com, msg, 'uint8');
    response = fread(com, 10, 'uint8' );
    result = response(2) == 129;
end 