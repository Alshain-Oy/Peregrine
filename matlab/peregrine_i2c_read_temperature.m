function result = peregrine_i2c_read_temperature( com, address, i2c_address )
    value = peregrine_do_action( com, address, 19, i2c_address, 0 );
    result = (double(value)/ 32) * 0.125;
end