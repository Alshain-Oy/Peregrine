function result = peregrine_read( com, address, key )
    msg = [ address 2 0 0 0 0 0 0 0 0 ];
    msg(3:6) = uint8( typecast( swapbytes(uint32(key)), 'uint8') ) ;
    
    fwrite(com, msg, 'uint8');
    response = fread(com, 10, 'uint8' );
    result = int32( swapbytes( typecast( uint8( response(7:10) ), 'int32' ) ) );
end 