local key = KEYS[1]
local type_if_not_exists = ARGV[1]
local top_of_list = tonumber(ARGV[2])
local get_old_value = tonumber(ARGV[3])
local value = ARGV[4]

local key_exist = redis.call("EXISTS", key)

if (key_exist == 0) then
  if (type_if_not_exists == 'null') then
    return
  elseif (type_if_not_exists == 'list') then
    redis.call("RPUSH", key, value)
  else
    redis.call("SADD", key, value)
  end
else -- key exists
  local value_type = redis.call("TYPE", key)
  local old_value

  if get_old_value == 1 then
    if value_type.ok == 'list' then
      old_value = redis.call("LRANGE", key, 0, -1)
    elseif value_type.ok == 'set' then
      old_value = redis.call("SMEMBERS", key)
    end
  end

  -- Add new value depending on the type
  if value_type.ok == 'set' then
    redis.call("SADD", key, value)
  elseif value_type.ok == 'list' then
    if top_of_list == 1 then
      redis.call("LPUSH", key, value)
    else
      redis.call("RPUSH", key, value)
    end
  end

  return {old_value, value_type.ok}
end
