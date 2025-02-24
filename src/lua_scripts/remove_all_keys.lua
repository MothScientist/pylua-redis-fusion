local get_count_keys = ARGV[1] == "1"
local total_keys = 0
local databases = tonumber(redis.call('CONFIG', 'GET', 'databases')[2])

for i = 0, databases - 1 do
    redis.call('SELECT', i)
    local db_size = redis.call('DBSIZE')
    total_keys = total_keys + db_size
end

if get_count_keys then
  for i = 0, databases - 1 do
    redis.call('SELECT', i)
    local db_size = redis.call('DBSIZE')
    total_keys = total_keys + db_size
  end
end

redis.call("FLUSHALL")

return total_keys
