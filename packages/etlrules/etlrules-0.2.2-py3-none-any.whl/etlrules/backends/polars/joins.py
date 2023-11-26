from etlrules.backends.common.joins import (
    LeftJoinRule as LeftJoinRuleBase,
    RightJoinRule as RightJoinRuleBase,
    InnerJoinRule as InnerJoinRuleBase,
    OuterJoinRule as OuterJoinRuleBase,
)


class JoinsMixin():
    def do_apply(self, left_df, right_df):
        return self.do_join(left_df, right_df, self.suffixes)

    def do_join(self, left_df, right_df, suffixes):
        left_on, right_on = self._get_key_columns()
        suffix_left, suffix_right = suffixes
        common_cols = [col for col in left_df.columns if col in right_df.columns]
        df = left_df.join(
            right_df,
            how=self.JOIN_TYPE,
            left_on=left_on,
            right_on=right_on,
            suffix=suffix_right or "_right"
        )
        if suffix_left:
            df = df.rename(
                {col: col + suffix_left for col in common_cols if col not in left_on}
            )
        if not suffix_right:
            df = df.rename({
                col + "_right": col for col in common_cols if col not in right_on
            })
        else:
            # polars doesn't create suffixes for keys in the right_on (when they dont match the left_on keys)
            # pandas does, so replicating that behavior
            right_only = {right: left for right, left in zip(right_on, left_on) if right != left}
            if right_only:
                df = df.with_columns(
                    *[df[left].alias(right + suffix_right) for right, left in right_only.items()]
                )
        return df


class LeftJoinRule(JoinsMixin, LeftJoinRuleBase):
    JOIN_TYPE = "left"


class InnerJoinRule(JoinsMixin, InnerJoinRuleBase):
    JOIN_TYPE = "inner"


class OuterJoinRule(JoinsMixin, OuterJoinRuleBase):
    JOIN_TYPE = "outer"


class RightJoinRule(JoinsMixin, RightJoinRuleBase):
    JOIN_TYPE = "left"

    def do_apply(self, left_df, right_df):
        suffixes = reversed(self.suffixes)
        return super().do_join(right_df, left_df, suffixes)
