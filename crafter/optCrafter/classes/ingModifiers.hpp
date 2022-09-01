class ingModifiers {
public:
    ingModifiers() {
        left = right = above = under = touching = notTouching = 0;
    }

    void setValues(json values) {

    }

    const int   left,
                right,
                above,
                under,
                touching,
                notTouching;
};