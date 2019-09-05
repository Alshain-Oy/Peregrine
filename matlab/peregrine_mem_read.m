function result = peregrine_mem_read( com, address, position )
    result = peregrine_do_action( com, address, 32, position, 0 );
end