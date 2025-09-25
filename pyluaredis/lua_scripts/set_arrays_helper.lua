-- Set function for writing arrays (RPUSH/SADD)
local key = KEYS[1]
local get_old_value = tonumber(ARGV[1]) == 1
local time_ms = tonumber(ARGV[2])
local if_exist = tonumber(ARGV[3]) == 1
local if_not_exist = tonumber(ARGV[4]) == 1
local keep_ttl = tonumber(ARGV[5]) == 1

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


-- The unpack function in Lua is very limited (8000 elements)
-- -> split into chunks if the number of elements to be written exceeds 5000
local values
local set_operation = ARGV[6]
local without_chunks = tonumber(ARGV[7]) == 1
local start_argument = 8

if without_chunks then

  values = {unpack(ARGV, start_argument, #ARGV)}
  if set_operation == 'rpush' then
    redis.call("RPUSH", key, unpack(values))
  else
    redis.call("SADD", key, unpack(values))
  end

else

  local chunk_size = 7850
  local current_chunk = {}

  -- Function to write the current chunk to Redis
  local function write_chunk()
    if #current_chunk > 0 then
      if set_operation == 'rpush' then
        redis.call("RPUSH", key, unpack(current_chunk))
      else
        redis.call("SADD", key, unpack(current_chunk))
      end
        current_chunk = {} -- clear the current chunk
    end
  end

  -- Loop through all arguments containing the values you want to write
  for i = start_argument, #ARGV do
      table.insert(current_chunk, ARGV[i])
      -- Если текущий чанк достиг размера, записываем его в Redis
      if #current_chunk == chunk_size then
          write_chunk()
      end
  end

  write_chunk() -- record the remainder if it is not empty

end


-- if the key lifetime is defined
if time_ms > 0 then
   redis.call("PEXPIRE", key, time_ms)
end

return value
