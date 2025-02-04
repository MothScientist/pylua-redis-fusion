if redis.call('EXISTS', KEYS[1]) == 1 then
    redis.call('RENAME', KEYS[1], KEYS[2])
    return true
else
    return false
end