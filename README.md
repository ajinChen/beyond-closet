# Beyond Closet

*Final project of Product Analytics, USF MSDS program.*

# About

*Your imagination has no limits, and anything is possible for you to imagine!*

**CEO**: [Alan Wang](https://www.linkedin.com/in/alan-yuefan-wang/) <br>
**CTO**: [Ajin Chen](https://www.linkedin.com/in/jih-chin-chen/) <br>
**COO**: [Jeff Yeh](https://www.linkedin.com/in/jeffyeh1/) <br>
**Engineer**: [Ajin Chen](https://www.linkedin.com/in/jih-chin-chen/), [Karsten Cao](https://www.linkedin.com/in/karstencao/),
              [Yanan Cao](https://www.linkedin.com/in/yanancao21/), [Tong Wang](https://www.linkedin.com/in/tongwang028/), [Alan Wang](https://www.linkedin.com/in/alan-yuefan-wang/), [Ruifeng Luo](https://www.linkedin.com/in/ruifeng-luo/) <br>
**Data Scientist**:  [Kaihang Zhao](https://www.linkedin.com/in/kaihang-zhao/), [Yangzhou Tang](https://www.linkedin.com/in/yangzhou-tang/), [Chenjia Guo](https://www.linkedin.com/in/chenjia-guo/), [Fan Li](https://www.linkedin.com/in/victorlifan/) <br>
**Project Manager**:  [Monty Xu](https://www.linkedin.com/in/mengtingxu/), [Roger Ren](https://www.linkedin.com/in/zihaoren/), [Jeff Yeh](https://www.linkedin.com/in/jeffyeh1/) <br>


# Technical Components

In case of postgres db working weird, clean container and volume first.
```
docker container prune -f
docker volume prune -f
```

To spin up the container services, run the following, 
```
docker-compose build && docker-compose --env-file env_file up
```
