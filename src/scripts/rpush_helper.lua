local key = KEYS[1]
local time_ms = tonumber(ARGV[1])
local if_exist = tonumber(ARGV[2])
local if_not_exist = tonumber(ARGV[3])
local values = {unpack(ARGV, 3, #ARGV)}  -- the second parameter is the number of the last variable!

local key_exist = redis.call("EXISTS", key)


if (key_exist == 0 and if_exist == 1) or (key_exist == 1 and if_not_exist == 1) then
  return
end

-- before writing, we must clear the current value by key, if it exists
if key_exist == 1 then
  redis.call("DEL", key)
end

redis.call("RPUSH", key, unpack(values))

-- if the key lifetime is defined
if time_ms and time_ms > 0 then
   redis.call("PEXPIRE", key, time_ms_num)
end
