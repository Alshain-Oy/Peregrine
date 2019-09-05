function result = peregrine_move( com, address, target, speed, accel )
    msg = [ address 0 0 0 0 0 0 0 0 0 ];
    msg(3:6) = uint8( typecast( swapbytes(int32(target)), 'uint8') ) ;
    msg(7:8) = uint8( typecast( swapbytes(int16(speed/32)), 'uint8') );
    msg(9:10) = uint8( typecast( swapbytes(uint16(accel)), 'uint8') );
    
    fwrite(com, msg, 'uint8');
    response = fread(com, 10, 'uint8' );
    result = response(2) == 128;
end 