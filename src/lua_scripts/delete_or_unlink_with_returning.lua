local key = KEYS[1]
local returning = ARGV[1] == "1"
local delete_or_unlink = ARGV[2]
local value

if returning then
  local value_type = redis.call("TYPE", key) -- determine what type the value stored in this key is

  if value_type.ok == 'string' then -- if value: bool/int/float/str
      value = redis.call("GET", key)
  elseif value_type.ok == 'list' then -- to get lists we use another function
      value = redis.call("LRANGE", key, 1, -1) -- special attention is required for the range
  end
end

if delete_or_unlink == 'delete' then
  redis.call("DEL", key)
else
  redis.call("UNLINK", key)
end
  

if returning then
  return value
end