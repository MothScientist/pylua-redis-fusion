local key = KEYS[1]
local res

local value_type = redis.call("TYPE", key) -- determine what type the value stored in this key is

if value_type.ok == 'string' then -- if value: bool/int/float/str
    res = redis.call("GET", key)
elseif value_type.ok == 'list' then -- to get lists we use another function
    res = redis.call("LRANGE", key, 1, -1) -- special attention is required for the range
else
    res = nil
end

return res
