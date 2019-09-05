function result = peregrine_mem_write( com, address, position, value )
    result = peregrine_do_action( com, address, 25, position, value );
end