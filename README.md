# KrazyC
C on steroids ... sort of ... maybe

## How to use
KrazyC (`.kc`) transpiles to C using the transpiler provided
```
python3 transpiler.py myfile.kc
```
It's still not mature so issues are welcomed

## Indentation
We know indentation in Python sucks, that's why we are bringing it to C!
```C
int main():
    printf("Hi!");
    return 0;
```
We don't want to upset too many people tho, therefore braces still work:
```C
int main() {
    printf("Hi!");
    return 0;
}
```
In fact, you can mix them:
```C
int main():
    if (1 + 1 == 2):
        printf("Hi!");
    if (1 + 2 == 3) {
        printf("Hello");
    }
    return 0;
```
Amazing right?
## Goto
Don't use `goto`.
```C
int main() {
    goto label;
    label:
        printf("nope");
}
```
```
Transpiler Error:
    No gotos thanks
Line 4 | goto label;
```

## Todo
- Write the transpiler in C
- Write the transpiler in KrazyC
- Write a "compiler" where it just transpiles and use gcc
- World domination
