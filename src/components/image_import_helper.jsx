const paintings = import.meta.glob('../public/images/*.png', {eager: true})

export const imageMap = Object.fromEntries(
    Object.entries(paintings).map(([path, module])  => [
        path.split('/').pop(),
        module.default
    ])
)