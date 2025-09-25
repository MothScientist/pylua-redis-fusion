local keys = KEYS

for _, key in ipairs(keys) do
    redis.call("PERSIST", key)
end