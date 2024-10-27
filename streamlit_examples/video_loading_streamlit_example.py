import os

import matplotlib.pyplot as plt
import torch
from mpl_toolkits.axes_grid1 import ImageGrid
from torchvision import transforms

from kale.loaddata.videos import VideoFrameDataset
from kale.prepdata.video_transform import ImglistToTensor
from kale.utils.download import download_file_gdrive


def plot_video(rows, cols, frame_list, plot_width, plot_height):
    fig = plt.figure(figsize=(plot_width, plot_height))
    grid = ImageGrid(
        fig,
        111,  # similar to subplot(111)
        nrows_ncols=(rows, cols),  # creates 2x2 grid of axes
        axes_pad=0.3,  # pad between axes in inch.
    )

    for index, (ax, im) in enumerate(zip(grid, frame_list)):
        # Iterating over the grid returns the Axes.
        ax.imshow(im)
        ax.set_title(index)
    plt.show()

def denormalize(video_tensor):
    """
    Undoes mean/standard deviation normalization, zero to one scaling,
    and channel rearrangement for a batch of images.
    args:
        video_tensor: a (FRAMES x CHANNELS x HEIGHT x WIDTH) tensor
    """
    inverse_normalize = transforms.Normalize(
        mean=[-0.485 / 0.229, -0.456 / 0.224, -0.406 / 0.225], std=[1 / 0.229, 1 / 0.224, 1 / 0.225]
    )
    return (inverse_normalize(video_tensor) * 255.0).type(torch.uint8).permute(0, 2, 3, 1).numpy()


def demo_1():
    videos_root = os.path.join(os.getcwd(), "demo_dataset")
    annotation_file = os.path.join(videos_root, "annotations.txt")

    dataset = VideoFrameDataset(
        root_path=videos_root,
        annotationfile_path=annotation_file,
        num_segments=5,
        frames_per_segment=1,
        imagefile_template="img_{:05d}.jpg",
        transform=None,
        random_shift=True,
        test_mode=False,
    )

    sample = dataset[0]
    frames = sample[0]  # list of PIL images

    plot_video(rows=1, cols=5, frame_list=frames, plot_width=15.0, plot_height=3.0)


def demo_2():
    videos_root = os.path.join(os.getcwd(), "demo_dataset")
    annotation_file = os.path.join(videos_root, "annotations.txt")

    dataset = VideoFrameDataset(
        root_path=videos_root,
        annotationfile_path=annotation_file,
        num_segments=1,
        frames_per_segment=9,
        imagefile_template="img_{:05d}.jpg",
        transform=None,
        random_shift=True,
        test_mode=False,
    )

    sample = dataset[1]
    frames = sample[0]  # list of PIL images
    label = sample[1]  # integer label

    plot_video(rows=3, cols=3, frame_list=frames, plot_width=10.0, plot_height=5.0)


def demo_3():
    videos_root = os.path.join(os.getcwd(), "demo_dataset")
    annotation_file = os.path.join(videos_root, "annotations.txt")
    frames = sample[0]  

    preprocess = transforms.Compose(
        [
            ImglistToTensor(),  # list of PIL images to (FRAMES x CHANNELS x HEIGHT x WIDTH) tensor
            transforms.Resize(299),  # image batch, resize smaller edge to 299
            transforms.CenterCrop(299),  # image batch, center crop to square 299x299
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    dataset = VideoFrameDataset(
        root_path=videos_root,
        annotationfile_path=annotation_file,
        num_segments=5,
        frames_per_segment=1,
        imagefile_template="img_{:05d}.jpg",
        transform=preprocess,
        random_shift=True,
        test_mode=False,
    )

    sample = dataset[1]
    frame_tensor = sample[0]  # tensor of shape (NUM_SEGMENTS*FRAMES_PER_SEGMENT) x CHANNELS x HEIGHT x WIDTH
    frames = sample[0]  

    print("Video Tensor Size:", frame_tensor.size())

    frame_tensor = denormalize(frame_tensor)
    plot_video(rows=1, cols=5, frame_list=frames, plot_width=15.0, plot_height=3.0)


    dataloader = torch.utils.data.DataLoader(
        dataset=dataset, batch_size=2, shuffle=True, num_workers=4, pin_memory=True
    )

    for epoch in range(10):
        for video_batch, labels in dataloader:
            print(labels)
            print("\nVideo Batch Tensor Size:", video_batch.size())
            print("Batch Labels Size:", labels.size())
            break
        break

def demo_4():
    videos_root = os.path.join(os.getcwd(), "demo_dataset_multilabel")
    annotation_file = os.path.join(videos_root, "annotations.txt")

    preprocess = transforms.Compose(
        [
            ImglistToTensor(),  # list of PIL images to (FRAMES x CHANNELS x HEIGHT x WIDTH) tensor
            transforms.Resize(299),  # image batch, resize smaller edge to 299
            transforms.CenterCrop(299),  # image batch, center crop to square 299x299
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    dataset = VideoFrameDataset(
        root_path=videos_root,
        annotationfile_path=annotation_file,
        num_segments=5,
        frames_per_segment=1,
        imagefile_template="img_{:05d}.jpg",
        transform=preprocess,
        random_shift=True,
        test_mode=False,
    )

    dataloader = torch.utils.data.DataLoader(
        dataset=dataset, batch_size=3, shuffle=True, num_workers=2, pin_memory=True
    )

    print("\nMulti-Label Example")
    for epoch in range(10):
        for batch in dataloader:
            """
            Insert Training Code Here
            """
            video_batch, (labels1, labels2, labels3) = batch

            print("Video Batch Tensor Size:", video_batch.size())
            print("Labels1 Size:", labels1.size())  # == batch_size
            print("Labels2 Size:", labels2.size())  # == batch_size
            print("Labels3 Size:", labels3.size())  # == batch_size

            break
        break


def main():
    demo_1()





if __name__ == "__main__":
    main()