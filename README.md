# Predicting Out-of-Distribution Error with Confidence Optimal Transport

This repository is the official implementation of [Predicting Out-of-Distribution Error with Confidence Optimal Transport](https://openreview.net/forum?id=dNGxmwRpFyG). If you find this repository useful or use this code in your research, please cite the following paper: 

> Lu, Y., Wang, Z., Zhai, R., Kolouri, S., Campbell, J., & Sycara, K. (2023). Predicting Out-of-Distribution Error with Confidence Optimal Transport. ICLR 2023 Workshop on Pitfalls of limited data and computation for Trustworthy ML.

```
@inproceedings{
    title={Predicting Out-of-Distribution Error with Confidence Optimal Transport},
    author={Yuzhe Lu, Zhenlin Wang, Runtian Zhai, Soheil Kolouri, Joseph Campbell and Katia P. Sycara},
    booktitle={ICLR 2023 Workshop on Pitfalls of limited data and computation for Trustworthy ML},
    year={2023},
}
```

```run_estimation.py``` contains implementation of COT (line 99-106). 

```train_model.py``` trains models for which to estimate performance. 

```notebooks``` gather results and make visualizations. 