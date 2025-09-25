local key = KEYS[1]
if redis.call('EXISTS', key) == 1 then
    redis.call('RENAME', key, KEYS[2])
    return true
else
    return false
end