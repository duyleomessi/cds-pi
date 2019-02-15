# Quy ước tên sân
```
Sân đỏ: 'R'
Sân xanh: 'G'
```

# Quy ước góc của servo:
```
Quay trái: 'LEFT'
Quay nghiêng sang trái: 'STRAIGH_LEFT'
Quay phải: 'RIGHT'
Quay nghiêng sang phải: 'STRAIGH_RIGHT'
```

# Quy ước bản tin

## Tín hiệu bắt đầu dừng và reset trận đấu

### Bắt đầu thi đấu 
```
Action: subscribe
Topic: 'cds/command'
Data: 
{
    'command': 'RACE_START_1'
}
```

### Dừng trận đấu
```
Action: subscribe
Topic: 'cds/command'
Data: 
{
    'command': 'RACE_STOP_1'
}
```

### Reset trận đấu
```
Action: subscribe
Topic: 'cds/command'
Data: 
{
    'command': 'RACE_RESET_1'
}
```

## Tín hiệu sensor
```
Action: publish
Topic: 'cds/sensor'
Data: 
{
    'stadium': stadium, 
    'channel': channel, 
    'runtime': runtime
}
```

Ví dụ

```
{
    'stadium': 'R', 
    'channel': '1', 
    'runtime': '0:23' 
}
```

Khi bắt đầu và reset trận đấu thời gian là: 'START:START' 

```
{
    'stadium': 'R', 
    'channel': '1', 
    'runtime': '0:23' or runtime: 'START:START'
}
```

## Điều khiển servo

Để điều khiển servo trên server sẽ publish một bản tin xuống client(pi):

```
Action: subscribe
Topic: 'cds/servo/command'
Data:
{
    "stadium": stadium,
    "servo": servo,
    "angle": angle
}
```

Ví dụ muốn quay servo 1  ở sân xanh sang trái:
```
{
    'stadium': 'G',
    'servo': 1,
    'angle': 'LEFT'
}
```

Khi bắt đầu trận đấu, server sẽ gửi bản tin xuống client(pi) để pi quay servo. Khi client nhận được thông báo cuộc thi bắt đầu, sẽ quay servo và gửi 1 bản 
tin lên server thông báo cho server servo quay hướng nào. Bản tin được định nghĩa như sau:
```
Action: publish
Topic: 'cds/servo/state'
Data: 
{
    "stadium": stadiumConfig.STADIUM, 
    "servo": servo, 
    "state": state
}
```

Ví dụ:
Để thông báo cho server biết servo 2 quay phải ta publish lên server bản tin:
```
{
    "stadium": 'R', 
    "servo": 2, 
    "state": 'RIGHT'
}
```