-- Set function for writing arrays (RPUSH/SADD)
local key = KEYS[1]
local get_old_value = tonumber(ARGV[1]) == 1
local time_ms = tonumber(ARGV[2])
local if_exist = tonumber(ARGV[3]) == 1
local if_not_exist = tonumber(ARGV[4]) == 1
local keep_ttl = tonumber(ARGV[5]) == 1
local set_operation = ARGV[6]
local values = {unpack(ARGV, 7, #ARGV)}

local key_exist = redis.call("EXISTS", key) == 1

if key_exist and keep_ttl then
  time_ms = redis.call("PTTL", key)
end


if (not key_exist and if_exist) or (key_exist and if_not_exist) then
  return
end

local value

if get_old_value then
  local value_type = redis.call("TYPE", key) -- determine what type the value stored in this key is

  if value_type.ok == 'string' then -- if value: bool/int/float/str
    value = redis.call("GET", key)
  elseif value_type.ok == 'list' then -- to get lists we use another function
    value = redis.call("LRANGE", key, 0, -1) -- special attention is required for the range
  elseif value_type.ok == 'set' then
    value = redis.call("SMEMBERS", key)
  end
end

-- before writing, we must clear the current value by key, if it exists
if key_exist then
  redis.call("DEL", key)
end

if set_operation == 'rpush' then
  redis.call("RPUSH", key, unpack(values))
else
  redis.call("SADD", key, unpack(values))
end

-- if the key lifetime is defined
if time_ms > 0 then
   redis.call("PEXPIRE", key, time_ms)
end

return value
