local keys = KEYS
local delete_or_unlink = ARGV[1]

local result = {} -- to store existing keys in {key:value} format

for _, key in ipairs(keys) do
    local value
    local value_type = redis.call("TYPE", key) -- determine what type the value stored in this key is

    if value_type.ok == 'string' then -- if value: bool/int/float/str
      value = redis.call("GET", key)
    elseif value_type.ok == 'list' then -- to get lists we use another function
      value = redis.call("LRANGE", key, 0, -1) -- special attention is required for the range
    elseif value_type.ok == 'set' then
      value = redis.call("SMEMBERS", key)
    end

    if value then
        result[key] = value

        if delete_or_unlink == 'delete' then
          redis.call("DEL", key)
        else
          redis.call("UNLINK", key)
        end

    end
end

return cjson.encode(result)