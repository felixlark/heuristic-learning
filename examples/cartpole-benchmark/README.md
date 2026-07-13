# CartPole 研究进阶实验

这个可选实验把透明策略放进真实 Gymnasium 环境，并用固定种子隔离开发、保留和审计评估。

```bash
python3 -m pip install 'gymnasium[classic-control]'
npm run examples:cartpole:dev
npm run examples:cartpole:audit
```

先在 `dev` 上观察和修改策略。`holdout` 只用于冻结方案后的比较，`audit` 用于最后一次独立检查。每次运行都会向 `experiments/cartpole/trials.jsonl` 追加记录，不覆盖失败结果。

测试路径：`tests/test_cartpole_benchmark.py`。
