# imgread-testdata

Microscopy data files for testing imgread.

A test file from OME and 3 files I have been working with:

- lif 5 series, 3 channels, 41 z
- exp2 ometiff from imic1 with 2 channels, 81 time points
- t4_1 ometiff from imic2 with 4 channels, 3 timepoints and 5 x 3 tiles?
  dati marta efrem 24

I will check this number first together with:

- x, y dimension
- x resolution
- time resolution

I will the investigate ROI metadata.

Start with writing tests.

## development

```
git submodule add git@gin.g-node.org:/darosio/imgread-testdata.git tests/testdata

cd tests/testdata/
git annex init
git annex import ../data/LC26GFP_1.tf8
git commit -m "…"
git push (origin master)
git-annex push

cd ../../
git add .
(git submodule update --remote --merge)
git commit -m “…”
git push
```

git submodule update --init --recursive
git config annex.sshcaching true
cd tests/data/
git annex pull
