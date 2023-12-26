# Predicting Out-of-Distribution Error with Confidence Optimal Transport

Update: our latest work that extends this workshop paper, [Characterizing Out-of-Distribution Error via Optimal Transport](https://openreview.net/forum?id=dz5X8hnfJc&referrer=%5BAuthor%20Console%5D(%2Fgroup%3Fid%3DNeurIPS.cc%2F2023%2FConference%2FAuthors%23your-submissions)) is accepted at NeurIPS 2023, where we provide formal proofs of why COT works so well and present an even stronger method, Confidence Optimal Transport with Thresholding (COTT) to predict OOD error. The code can be found [here](https://github.com/luyuzhe111/COT)

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
