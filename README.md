# Beyond Closet

Beyond Closet is an awesome web application to get the color recommendation based on uploaded images and the color wheel theorem.

## About

*Your imagination has no limits, and anything is possible for you to imagine!*

**CEO**: [Alan Wang](https://www.linkedin.com/in/alan-yuefan-wang/) <br>
**CTO**: [Ajin Chen](https://www.linkedin.com/in/jih-chin-chen/) <br>
**COO**: [Jeff Yeh](https://www.linkedin.com/in/jeffyeh1/) <br>
**Engineer**: [Ajin Chen](https://www.linkedin.com/in/jih-chin-chen/), [Karsten Cao](https://www.linkedin.com/in/karstencao/),
              [Yanan Cao](https://www.linkedin.com/in/yanancao21/), [Tong Wang](https://www.linkedin.com/in/tongwang028/), [Alan Wang](https://www.linkedin.com/in/alan-yuefan-wang/), [Ruifeng Luo](https://www.linkedin.com/in/ruifeng-luo/) <br>
**Data Scientist**:  [Kaihang Zhao](https://www.linkedin.com/in/kaihang-zhao/), [Yangzhou Tang](https://www.linkedin.com/in/yangzhou-tang/), [Chenjia Guo](https://www.linkedin.com/in/chenjia-guo/), [Fan Li](https://www.linkedin.com/in/victorlifan/) <br>
**Project Manager**:  [Monty Xu](https://www.linkedin.com/in/mengtingxu/), [Roger Ren](https://www.linkedin.com/in/zihaoren/), [Jeff Yeh](https://www.linkedin.com/in/jeffyeh1/) <br>

## Requirements

* docker & docker-compose
* AWS account (S3, Elastic Beanstalk, Lambda, SageMaker)


## Technical Components

To launch the container services of app, run the following:
```bash
# launch application
docker-compose build && docker-compose --env-file env_file up

# shut-down application
docker-compose down
```

## High Level Archiecure

<img src="https://s2.loli.net/2022/07/21/BVb3xWKGMemn1wQ.png" alt="image-20220720122559481" style="zoom:50%;" />

## ML Algorithms behind the Website

* Object Segmentation (UNet)

* Color Detection (Kmeans++)

* Color Wheel Theorem (Projecting to spherical color space)

## Website Demo

<img src="https://s2.loli.net/2022/07/21/yLe5DfV2MJ4cqt9.png" alt="image-20220720130029459" style="zoom:50%;" />

<img src="https://s2.loli.net/2022/07/21/moLRGcNuCHJfVz2.png" alt="image-20220720130140829" style="zoom:50%;" />

<img src="https://s2.loli.net/2022/07/21/qdNaAYmixHOzubX.png" alt="image-20220720130230891" style="zoom:50%;" />

