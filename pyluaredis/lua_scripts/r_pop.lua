local key = KEYS[1]
local count = tonumber(ARGV[1])
local reverse = tonumber(ARGV[2]) == 1

local key_exist = redis.call("EXISTS", key)
if key_exist ~= 1 then
  return
end

local len
local value_type = redis.call("TYPE", key)

if value_type.ok == 'list' then

  -- List ------------------------------
  len = redis.call("LLEN", key)
  if len >= count then -- if need to get 1 element from non-empty list
    if reverse then
      return redis.call("LPOP", key, count)
    else
      return redis.call("RPOP", key, count)
    end
  end
  --------------------------------------

elseif value_type.ok == 'set' then

  -- Set --------------------------------
  len = redis.call("SCARD", key)
  if len >= count then -- if need to get <count> elements from non-empty set
    return redis.call("SPOP", key, count)
  end
  ---------------------------------------

else
  return
end

