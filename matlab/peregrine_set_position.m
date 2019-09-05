function result = peregrine_set_position( com, address, position )
    result = peregrine_do_action( com, address, 48, 0, position );
end