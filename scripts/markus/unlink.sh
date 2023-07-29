for symlink_file in ~/git/LLaVa/checkpoints/llava-7b-pretrain/*; do
    if [ -L "$symlink_file" ]; then
        # Get the target file path
        target_file=$(readlink "$symlink_file")
        # Copy the content from the target file to the destination
        cp "$target_file" /path/to/destination/
        # Unlink (remove) the symlink
        unlink "$symlink_file"
    fi
done
