local key = KEYS[1]

local key_exist = redis.call("EXISTS", key)
if key_exist ~= 1 then
  return
end

local value_type = redis.call("TYPE", key)
if value_type.ok == 'list' then
  return redis.call("LLEN", key)
elseif value_type.ok == 'set' then
  return redis.call("SCARD", key)
else
  return 0
end

