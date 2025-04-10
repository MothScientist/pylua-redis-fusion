-- function to get values by key
local key = KEYS[1]
local key_exist = redis.call("EXISTS", key) == 1

if not key_exist then
  return {nil, nil}
end

local value
local value_type = redis.call("TYPE", key) -- determine what type the value stored in this key is

if value_type.ok == 'string' then -- if value: bool/int/float/str
  value = redis.call("GET", key)
elseif value_type.ok == 'list' then -- to get lists we use another function
  value = redis.call("LRANGE", key, 0, -1) -- special attention is required for the range
elseif value_type.ok == 'set' then
  value = redis.call("SMEMBERS", key)
end

return {value, value_type.ok}
