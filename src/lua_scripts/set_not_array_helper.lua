local key = KEYS[1]
local get_old_value = tonumber(ARGV[1])
local time_ms = tonumber(ARGV[2])
local if_exist = tonumber(ARGV[3])
local if_not_exist = tonumber(ARGV[4])
local keep_ttl = tonumber(ARGV[5])
local value = ARGV[6]

local res = nil


local key_exist = redis.call("EXISTS", key)


if key_exist == 1 and keep_ttl == 1 then
  time_ms = redis.call("PTTL", key)
end


if (key_exist == 0 and if_exist == 1) or (key_exist == 1 and if_not_exist == 1) then
  return
end

local res

if get_old_value == 1 then
  local value_type = redis.call("TYPE", key) -- determine what type the value stored in this key is

  if value_type.ok == 'string' then -- if value: bool/int/float/str
      res = redis.call("GET", key)
  elseif value_type.ok == 'list' then -- to get lists we use another function
      res = redis.call("LRANGE", key, 1, -1) -- special attention is required for the range
  end
end

-- before writing, we must clear the current value by key, if it exists
if key_exist == 1 then
  redis.call("DEL", key)
end

redis.call("SET", key, value)

-- if the key lifetime is defined
if time_ms > 0 then
   redis.call("PEXPIRE", key, time_ms)
end

return res