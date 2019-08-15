from mamba import description, context, it
from expects import expect, equal

with description('whatever') as self:
    with it('1 is 1'):
        expect(1).to(equal((1)))
