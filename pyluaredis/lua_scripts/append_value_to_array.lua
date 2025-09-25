local key = KEYS[1]
local index = tonumber(ARGV[1])
local type_if_not_exists = ARGV[2] -- 'null', 'list' or 'set'
local get_old_value = tonumber(ARGV[3]) == 1
local value = ARGV[4]

local key_exist = redis.call("EXISTS", key)

if (key_exist == 0) then
  if (type_if_not_exists == 'null') then
    return {nil, nil}
  elseif (type_if_not_exists == 'list') then
    redis.call("RPUSH", key, value)
  else
    redis.call("SADD", key, value)
  end
else -- key exists
  local value_type = redis.call("TYPE", key)
  local old_value

  if get_old_value then
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
    if index == 0 then
      redis.call("LPUSH", key, value)
    elseif index == -1 then
      redis.call("RPUSH", key, value)
    else
      local length = redis.call('LLEN', key)
      if index >= length then
        redis.call('RPUSH', key, value)
      else
        -- Insert element by index -----------------------------
        local temp = {}
        -- Remove elements from the tail until we reach the desired position
        for _ = length - 1, index, -1 do
            temp[#temp + 1] = redis.call('RPOP', key)
        end

        -- Insert the new element
        redis.call('RPUSH', key, value)

        -- Put back the removed elements in reverse order
        for i = #temp, 1, -1 do
            redis.call('RPUSH', key, temp[i])
        end
        --------------------------------------------------------
      end
    end
  end

  return {old_value, value_type.ok}
end
