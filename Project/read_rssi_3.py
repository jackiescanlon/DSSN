bd_address = 'FC:58:FA:8E:12:78'
interval = 1    

id = bd_address.split(':').reverse.join(' ')
found = false

t3 = Time.now + interval

IO.popen('sudo hcidump --raw').each_line do |x| 
  
  found = if found then

    rssi = (x.split.last.hex - 256).to_s
    h = {bdaddress: bd_address, rssi: rssi}

    if t3 < Time.now then
      puts h.inspect
      t3 = Time.now + interval
    end

    false

  else
    x.include?(id)
  end

end
